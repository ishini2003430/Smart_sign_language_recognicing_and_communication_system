import React, { useContext, useEffect, useState, createContext } from 'react';

const ThemeContext = createContext({ theme:'light', setTheme:()=>{} });
export function ThemeProvider({children}) {
  const [theme,setTheme] = useState(()=>{
    try {return localStorage.getItem('slsl-theme') === 'dark' ? 'dark' : 'light';} catch {return 'light';}
  });
  useEffect(()=>{
    document.documentElement.setAttribute('data-theme', theme);
    try {localStorage.setItem('slsl-theme',theme);} catch {}
  },[theme]);
  useEffect(()=>{
    try {
      document.documentElement.classList.toggle('high-contrast',localStorage.getItem('slsl-contrast') === 'high');
      document.documentElement.classList.toggle('large-text',localStorage.getItem('slsl-large-text') === '1');
    } catch {}
  },[]);
  return <ThemeContext.Provider value={{theme,setTheme}}>{children}</ThemeContext.Provider>;
}
function ThemeButton({research=false}) {
  const {theme,setTheme}=useContext(ThemeContext);
  const label=theme==='dark'?'Light mode':'Dark mode';
  return <button type="button" className="theme-toggle" data-react-theme="1" aria-label={label}
    style={research?{width:'100%',marginTop:'14px',background:'rgba(255,255,255,0.06)',color:'#E5E7EB',borderColor:'rgba(255,255,255,0.12)'}:undefined}
    onClick={()=>setTheme(theme==='dark'?'light':'dark')}>
    <span aria-hidden="true">{theme==='dark'?'☀️':'🌙'}</span><span className="theme-toggle-label">{label}</span>
  </button>;
}
export function useTheme(){return useContext(ThemeContext);}
const userLinks=[
 ['dashboard','Dashboard'], ['recognition','Recognition'], ['translation','Translation'],
 ['learn','Learn SLSL'], ['communication','Communication'], ['library','Signs'],
 ['history','History'], ['progress','Progress']
];
const researchLinks=[
 ['research-dashboard','⌂','Dashboard'], ['recognition-analysis','▥','Recognition Analysis'],
 ['dataset','◎','Dataset Management'], ['research-evaluation','▤','Research Evaluation']
];
export function UserNav(){
 const path=window.location.pathname.slice(1);
 return <header className="user-nav" id="user-nav">
  <a className="user-brand" href="/dashboard"><span className="user-brand-logo">🤟</span><span className="user-brand-text"><strong>SLSL</strong><small>Smart Communication</small></span></a>
  <nav className="user-nav-links" aria-label="Main navigation">
   {userLinks.map(([key,label])=><a key={key} href={'/'+key} className={path===key?'active':''}>{label}</a>)}
  </nav>
  <div className="user-nav-actions">
   <ThemeButton/>
   <a className="icon-link" href="/settings" title="Settings" aria-label="Settings">⚙</a>
   <a className="profile-link" href="/profile"><span className="nav-avatar">K</span><span className="nav-profile-copy"><strong>Kamani</strong><small>Demo User</small></span></a>
   <a className="logout-link" href="/">Logout</a>
  </div>
 </header>;
}
export function ResearchSidebar(){
 const path=window.location.pathname.slice(1);
 return <aside className="research-sidebar" id="research-sidebar">
  <a className="research-brand" href="/research-dashboard"><span className="research-brand-logo">🤟</span><span><strong>SLSL</strong><small>Research Console</small></span></a>
  <div className="research-nav-label">Research Modules</div>
  <nav className="research-nav">{researchLinks.map(([key,icon,label])=><a key={key} href={'/'+key} className={path===key?'active':''}><span>{icon}</span>{label}</a>)}</nav>
  <div className="research-nav-label">Prototype Preview</div>
  <nav className="research-nav compact">
   <a href="/recognition"><span>📷</span>User Recognition</a>
   <a href="/communication"><span>💬</span>User Communication</a>
   <a href="/learn"><span>🎓</span>User Learning</a>
  </nav>
  <div className="research-sidebar-note"><strong>Research Workspace</strong><p>Experimental results are preliminary until measured on held-out data.</p></div>
  <ThemeButton research />
  <a className="research-logout" href="/">⇥ Logout</a>
 </aside>;
}
