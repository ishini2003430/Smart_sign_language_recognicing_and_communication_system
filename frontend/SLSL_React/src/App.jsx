import React, {useEffect,useState} from 'react';
import {ThemeProvider, useTheme} from './components/Navigation';
import {navigate} from './navigation';
import SettingsPage from "./pages/SettingsPage";
import ResearchDashboardPage from "./pages/ResearchDashboardPage";
import ProgressPage from "./pages/ProgressPage";
import HistoryPage from "./pages/HistoryPage";
import SignupPage from "./pages/SignupPage";
import DatasetPage from "./pages/DatasetPage";
import ErrorAnalysisPage from "./pages/ErrorAnalysisPage";
import ResearchEvaluationPage from "./pages/ResearchEvaluationPage";
import RecognitionAnalysisPage from "./pages/RecognitionAnalysisPage";
import RecognitionPage from "./pages/RecognitionPage";
import LibraryPage from "./pages/LibraryPage";
import IndexPage from "./pages/IndexPage";
import TranslationPage from "./pages/TranslationPage";
import CommunicationPage from "./pages/CommunicationPage";
import ProfilePage from "./pages/ProfilePage";
import DashboardPage from "./pages/DashboardPage";
import LearnPage from "./pages/LearnPage";
const pages={
  "/settings": SettingsPage,
  "/research-dashboard": ResearchDashboardPage,
  "/progress": ProgressPage,
  "/history": HistoryPage,
  "/signup": SignupPage,
  "/dataset": DatasetPage,
  "/error-analysis": ErrorAnalysisPage,
  "/research-evaluation": ResearchEvaluationPage,
  "/recognition-analysis": RecognitionAnalysisPage,
  "/recognition": RecognitionPage,
  "/library": LibraryPage,
  "/": IndexPage,
  "/translation": TranslationPage,
  "/communication": CommunicationPage,
  "/profile": ProfilePage,
  "/dashboard": DashboardPage,
  "/learn": LearnPage
};
const pageStyles={
  "/settings": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/research-dashboard": ["research-ui.css", "hud-research.css", "theme.css"],
  "/progress": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/history": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/signup": ["auth.css", "theme.css"],
  "/dataset": ["research-ui.css", "hud-research.css", "theme.css"],
  "/error-analysis": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/research-evaluation": ["research-ui.css", "hud-research.css", "theme.css"],
  "/recognition-analysis": ["research-ui.css", "hud-research.css", "theme.css"],
  "/recognition": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/library": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/": ["auth.css", "theme.css"],
  "/translation": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/communication": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/profile": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/dashboard": ["user-ui.css", "hud-theme.css", "theme.css"],
  "/learn": ["user-ui.css", "hud-theme.css", "theme.css"]
};

function RouteView(){
  const [path,setPath]=useState(window.location.pathname.replace(/\/$/,'') || '/');
  const {theme,setTheme}=useTheme();
  useEffect(()=>{
    const onRoute=()=>setPath(window.location.pathname.replace(/\/$/,'')||'/');
    window.addEventListener('popstate',onRoute);
    return ()=>window.removeEventListener('popstate',onRoute);
  },[]);
  useEffect(()=>{
    const actual=pages[path]?path:'/';
    const css=pageStyles[actual] || [];
    const links=css.map((name)=>{
      const link=document.createElement('link');link.rel='stylesheet';link.href='/styles/'+name;
      link.dataset.slslPageCss=actual;document.head.appendChild(link);return link;
    });
    document.body.dataset.page=actual.replace('/','');
    document.title=(actual==='/'?'Login':actual.substring(1).replaceAll('-',' '))+' — SLSL React';
    return ()=>{links.forEach(link=>link.remove());delete document.body.dataset.page;};
  },[path]);
  const onLinks=(e)=>{
    const target=e.target.closest('a[href]');
    if(!target || e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button!==0)return;
    const url=new URL(target.href,window.location.href);
    if(url.origin!==window.location.origin || !pages[url.pathname])return;
    e.preventDefault();navigate(url.pathname);
    window.scrollTo({top:0,left:0});
  };
  const onSettings=(e)=>{
    const themeBtn=e.target.closest('[data-set-theme]');
    if(themeBtn) setTheme(themeBtn.getAttribute('data-set-theme'));
    const button=e.target.closest('.theme-toggle');
    if(button && !button.dataset.reactTheme){
      // Non-navigation theme toggle in the preserved settings/login layout.
      setTheme(theme==='dark'?'light':'dark');
    }
  };
  const Page=pages[path] || pages['/'];
  return <div onClickCapture={onLinks} onClick={onSettings}><Page /></div>;
}
export default function App(){return <ThemeProvider><RouteView /></ThemeProvider>;}
