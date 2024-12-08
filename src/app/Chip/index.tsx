const Chip = ({className="", children}:{className?:string,children:React.ReactNode})=>{
    return (<div className={`rounded-md bg-neutral text-neutral-content py-0.5 px-2.5 border border-transparent text-sm transition-all shadow-sm ${className}`}>{children}</div>)
}

export const OutlinedChip =  ({className="", children}:{className?:string,children:React.ReactNode})=>{
    return <div className={`rounded-md border border-neutral-100 bg-base-100 text-base-900 py-0.5 px-2.5 text-center text-sm transition-all shadow-sm ${className}`}>
        {children}
  </div>
}

export default Chip;