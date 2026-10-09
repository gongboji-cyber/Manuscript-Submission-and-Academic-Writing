"""Draw one CSV-backed panel from a JSON specification. Never performs inference.

Usage: python plot_panel.py --data data.csv --spec panel.json --out panels/Fig2A
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import pandas as pd

from panel_tools import COLORS, export_panel, new_panel, panel_style, sha256

KINDS = ('strip', 'box', 'violin', 'paired', 'scatter', 'line', 'forest',
         'histogram', 'ecdf', 'heatmap', 'bar')


def draw_panel(data, spec):
    kind = spec['kind']
    if kind not in KINDS:
        raise ValueError('Supported kinds: '+', '.join(KINDS))
    columns = spec['columns']
    for role, name in columns.items():
        if name not in data:
            raise ValueError(f'Missing column for {role}: {name}')
        if role in ('label', 'group', 'id') and data[name].isna().any():
            raise ValueError(f'Missing {role} labels require explicit handling')
    def numeric(role):
        result = pd.to_numeric(data[columns[role]], errors='raise')
        if np.isinf(result.to_numpy(dtype=float)).any():
            raise ValueError(f'Infinite values in {role}')
        return result
    y = numeric('y')
    fig, ax = new_panel(spec.get('width_mm', 89), spec.get('height_mm', 70))
    rng = np.random.default_rng(spec.get('seed', 20261009))
    report = {'rows': len(data), 'missing_y': int(y.isna().sum()), 'kind': kind}
    group_col = columns.get('group')
    if group_col and data[group_col].isna().any():
        raise ValueError('Missing group labels require explicit handling')
    groups = spec.get('order', list(pd.unique(data[group_col])) if group_col else ['Observed'])
    if group_col and set(groups) != set(pd.unique(data[group_col])):
        raise ValueError('order must include every observed group exactly once')
    if len(set(groups)) != len(groups):
        raise ValueError('Duplicated group order')
    masks = [data[group_col].eq(group) if group_col else pd.Series(True, index=data.index) for group in groups]
    report['group_nonmissing_n'] = {str(g): int(y[m].notna().sum()) for g,m in zip(groups,masks)}
    if kind in ('strip', 'box', 'violin'):
        samples = [y[m].dropna().to_numpy() for m in masks]
        if any(len(sample)==0 for sample in samples):
            raise ValueError('Empty group cannot be represented as a distribution')
        if kind == 'box':
            ax.boxplot(samples, positions=range(len(groups)), widths=0.45,
                       whis=1.5, showfliers=False, medianprops={'color':'black'},
                       boxprops={'linewidth':0.7}, whiskerprops={'linewidth':0.7}, capprops={'linewidth':0.7})
            report['whiskers'] = '1.5 IQR; all observations shown separately'
        if kind == 'violin':
            if any(len(v)<5 or np.ptp(v)==0 for v in samples):
                raise ValueError('Violin requires >=5 nonidentical observations per group; use strip instead')
            if 'density_support' not in spec:
                raise ValueError('Violin requires density_support=[lower,upper] (null for unbounded)')
            support = spec['density_support']
            lo, hi = support
            if any((lo is not None and np.min(v)<lo) or (hi is not None and np.max(v)>hi) for v in samples):
                raise ValueError('Values exceed specified density support')
            violins = ax.violinplot(samples, positions=range(len(groups)), showextrema=False,
                                    bw_method=spec.get('bandwidth', 'scott'))
            for i,body in enumerate(violins['bodies']):
                body.set_facecolor(COLORS[i%len(COLORS)])
                body.set_alpha(0.25)
            report['kde_bandwidth'] = spec.get('bandwidth','scott')
        for i, sample in enumerate(samples):
            ax.scatter(i+rng.uniform(-0.12,0.12,len(sample)), sample, s=10,
                       color=COLORS[i%len(COLORS)], alpha=0.7, linewidths=0)
        ax.set_xticks(range(len(groups)), [str(g) for g in groups])
    elif kind == 'paired':
        id_col = columns['id']
        if not group_col or len(groups)!=2 or data[id_col].isna().any():
            raise ValueError('paired requires real nonmissing ID and exactly two groups')
        if data.duplicated([id_col,group_col]).any():
            raise ValueError('Repeated ID-condition rows require separate handling, not averaging')
        work = data.assign(_value=y).pivot(index=id_col, columns=group_col, values='_value').reindex(columns=groups)
        report['complete_pairs'] = int(work.notna().all(axis=1).sum())
        report['incomplete_pairs'] = int(work.isna().any(axis=1).sum())
        for _, row in work.iterrows():
            ax.plot([0,1], row.to_numpy(), color='#777777', alpha=0.35, linewidth=0.6)
        for i,g in enumerate(groups):
            ax.scatter(np.full(work[g].notna().sum(),i),work[g].dropna(),s=10,color=COLORS[i])
        ax.set_xticks([0,1],[str(g) for g in groups])
    elif kind in ('scatter','line','histogram','ecdf'):
        x = numeric('x') if kind in ('scatter','line') else None
        all_values = y.dropna().to_numpy()
        if len(all_values)==0:
            raise ValueError('No observed values')
        edges = np.histogram_bin_edges(all_values,bins=spec.get('bins','auto')) if kind=='histogram' else None
        for i,(g,m) in enumerate(zip(groups,masks)):
            color=COLORS[i%len(COLORS)]
            values = y[m]
            if kind=='scatter':
                valid = values.notna() & x[m].notna()
                ax.scatter(x[m][valid], values[valid], s=12, marker=['o','s','^','D'][i%4], color=color,alpha=0.75,label=str(g))
            elif kind=='line':
                if x[m].isna().any() or x[m].duplicated().any():
                    raise ValueError('line requires unique observed x within each series; split real trajectories explicitly')
                order = np.argsort(x[m].to_numpy())
                xx=x[m].to_numpy()[order]; yy=values.to_numpy()[order]
                if 'expected_x' in spec:
                    expected=np.asarray(spec['expected_x'],dtype=float)
                    if len(expected)==0 or np.any(~np.isfinite(expected)) or np.any(np.diff(expected)<=0) or not np.isin(xx,expected).all():
                        raise ValueError('expected_x must be unique, ascending and include every observed x')
                    series=pd.Series(yy,index=xx).reindex(spec['expected_x'])
                    xx=series.index.to_numpy(); yy=series.to_numpy()
                ax.plot(xx,yy,marker=['o','s','^','D'][i%4],markersize=3,
                        linestyle=['-','--','-.',':'][i%4],color=color,label=str(g))
                if 'low' in columns or 'high' in columns:
                    if not spec.get('uncertainty') or 'low' not in columns or 'high' not in columns:
                        raise ValueError('CI band needs both bounds and an uncertainty definition')
                    low=numeric('low')[m].to_numpy()[order]; high=numeric('high')[m].to_numpy()[order]
                    if np.any(low>high): raise ValueError('low exceeds high')
                    if 'expected_x' in spec:
                        low=pd.Series(low,index=x[m].to_numpy()[order]).reindex(xx).to_numpy()
                        high=pd.Series(high,index=x[m].to_numpy()[order]).reindex(xx).to_numpy()
                    low=np.where(np.isfinite(yy),low,np.nan); high=np.where(np.isfinite(yy),high,np.nan)
                    ax.fill_between(xx,low,high,color=color,alpha=0.15)
            elif kind=='histogram':
                ax.hist(values.dropna(),bins=edges,histtype='step',color=color,label=str(g))
                report['bin_edges']=edges.tolist()
            else:
                observed=np.sort(values.dropna().to_numpy())
                if len(observed)==0: raise ValueError('Empty ECDF group')
                unique,counts=np.unique(observed,return_counts=True)
                cumulative=np.cumsum(counts)/len(observed)
                ax.step(np.r_[unique[0],unique],np.r_[0,cumulative],where='post',color=color,
                        linestyle=['-','--','-.',':'][i%4],label=str(g))
                ax.set_ylim(0,1.03)
        if group_col:
            ax.legend(loc='upper left',bbox_to_anchor=(1.02,1),borderaxespad=0,frameon=False)
    elif kind=='forest':
        low,high = numeric('low'),numeric('high')
        if not spec.get('uncertainty'): raise ValueError('Define supplied uncertainty')
        if y.isna().any() or low.isna().any() or high.isna().any() or (low>high).any():
            raise ValueError('Forest estimates/bounds must be complete and ordered')
        pos=np.arange(len(data))
        ax.hlines(pos,low,high,color=COLORS[0],linewidth=1)
        ax.plot(y,pos,'o',color=COLORS[0],markersize=3)
        ax.vlines(low,pos-0.08,pos+0.08,color=COLORS[0],linewidth=0.7)
        ax.vlines(high,pos-0.08,pos+0.08,color=COLORS[0],linewidth=0.7)
        ax.set_yticks(pos,data[columns['label']].astype(str))
        ax.invert_yaxis()
        if spec.get('xscale')=='log' and ((low<=0).any() or (y<=0).any()):
            raise ValueError('Log forest requires positive values and bounds')
    elif kind=='heatmap':
        xcol=columns['x']; rowcol=columns['label']
        if data.duplicated([rowcol,xcol]).any(): raise ValueError('Heatmap duplicate cells cannot be implicitly averaged')
        matrix=data.assign(_value=y).pivot(index=rowcol,columns=xcol,values='_value')
        if 'vmin' not in spec or 'vmax' not in spec: raise ValueError('Heatmap needs explicit comparable color limits')
        norm=TwoSlopeNorm(vmin=spec['vmin'],vcenter=spec['center'],vmax=spec['vmax']) if 'center' in spec else None
        cmap=matplotlib.colormaps[spec.get('cmap','RdBu_r' if norm else 'cividis')].with_extremes(bad='#CCCCCC')
        mesh=ax.pcolormesh(np.ma.masked_invalid(matrix.to_numpy()),cmap=cmap,norm=norm,
                           vmin=None if norm else spec['vmin'],vmax=None if norm else spec['vmax'],rasterized=False)
        ax.set_xticks(np.arange(len(matrix.columns))+0.5,matrix.columns.astype(str))
        ax.set_yticks(np.arange(len(matrix.index))+0.5,matrix.index.astype(str))
        ax.invert_yaxis()
        colorbar=fig.colorbar(mesh,ax=ax,label=spec.get('colorbar_label',spec.get('ylabel','Value')))
        colorbar.ax.set_label('_colorbar')
        colorbar.solids.set_rasterized(False)
        report['matrix_missing_cells']=int(matrix.isna().sum().sum())
    else:
        if spec.get('bar_semantics') not in ('count','proportion'):
            raise ValueError('bar is for counts/proportions, not continuous means')
        if y.isna().any() or (y<0).any(): raise ValueError('Bar values must be nonnegative and complete')
        if spec['bar_semantics']=='proportion' and ((y>1).any() or not spec.get('denominator')):
            raise ValueError('Proportions require [0,1] and a denominator definition')
        labels=data[columns['label']].astype(str)
        if labels.duplicated().any(): raise ValueError('Bar categories must be unique')
        ax.bar(np.arange(len(data)),y,color=COLORS[0],width=0.65)
        ax.set_xticks(np.arange(len(data)),labels)
        ax.set_ylim(bottom=0)
    ax.set(xlabel=spec.get('xlabel',''),ylabel=spec.get('ylabel',''),title=spec.get('title',''))
    if spec.get('xscale')=='log':
        if kind not in ('scatter','line','forest'): raise ValueError('Log scale unsupported for this recipe')
        if kind in ('scatter','line') and (numeric('x').dropna()<=0).any(): raise ValueError('Nonpositive log-axis data')
        ax.set_xscale('log')
    if 'reference' in spec:
        reference=float(spec['reference'])
        if kind=='forest':
            if spec.get('xscale')=='log' and reference<=0: raise ValueError('Log reference must be positive')
            ax.axvline(reference,color='#777777',linestyle='--',linewidth=0.7,zorder=0)
        else:
            ax.axhline(reference,color='#777777',linestyle='--',linewidth=0.7,zorder=0)
    for axis in [ax.xaxis,ax.yaxis]:
        axis.label.set_clip_on(False)
    ax.title.set_clip_on(False)
    return fig,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',required=True,type=Path)
    parser.add_argument('--spec',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    spec=json.loads(args.spec.read_text(encoding='utf-8'))
    if not spec.get('question') or not spec.get('analysis_unit'):
        raise ValueError('Specify question and independent analysis_unit before plotting')
    if args.out.exists() and any(args.out.iterdir()) and not args.overwrite:
        raise FileExistsError('Panel directory is nonempty; use a fresh version')
    name=spec.get('panel_id',args.out.name)
    if not name or Path(name).name!=name or name in ('.','..') or '.' in name:
        raise ValueError('panel_id must be a simple filename without extension')
    data=pd.read_csv(args.data)
    with panel_style(spec.get('font','Arial')) as font_report:
        fig,report=draw_panel(data,spec)
        provenance={'question':spec['question'],'analysis_unit':spec['analysis_unit'],
                    'source':str(args.data.resolve()),'source_sha256':sha256(args.data),
                    'spec':spec,'data_checks':report,'fonts':font_report,
                    'pandas_version':pd.__version__}
        provenance['code_sha256']={filename:sha256(Path(__file__).resolve().parent/filename)
                                   for filename in ('plot_panel.py','panel_tools.py')}
        relative_data='data/source.csv' if spec.get('copy_input',True) else str(args.data.resolve())
        command=['python','code/plot_panel.py','--data',relative_data,'--spec','panel.json','--out','reproduced']
        provenance['reproduce_command']=command
        manifest=export_panel(fig,args.out/name,provenance=provenance,overwrite=args.overwrite)
        plt.close(fig)
    code=args.out/'code'; code.mkdir(exist_ok=True)
    for filename in ('plot_panel.py','panel_tools.py'):
        shutil.copy2(Path(__file__).resolve().parent/filename,code/filename)
    (args.out/'panel.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
    if spec.get('copy_input',True):
        folder=args.out/'data';folder.mkdir(exist_ok=True)
        shutil.copy2(args.data,folder/'source.csv')
    print(json.dumps({'panel':name,'automatic_status':manifest['automatic_status'],
                      'visual_review':'pending','font':font_report,'out':str(args.out.resolve())},ensure_ascii=False))


if __name__=='__main__':
    main()
