const Chip = ({className="", children}:{className?:string,children:React.ReactNode})=>{
    return (<div className={`rounded-md bg-slate-800 py-0.5 px-2.5 border border-transparent text-sm text-white transition-all shadow-sm ${className}`}>{children}</div>)
}

export const OutlinedChip =  ({className="", children}:{className?:string,children:React.ReactNode})=>{
    return <div className={`rounded-md border border-slate-300 py-0.5 px-2.5 text-center text-sm transition-all shadow-sm text-slate-600 ${className}`}>
        {children}
  </div>
}

export default Chip;