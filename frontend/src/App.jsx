import React, { useState, useEffect } from 'react';
import {
  DesktopOutlined,
  FileOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  DollarCircleOutlined,
  CalendarOutlined,
  LogoutOutlined,
  CheckCircleOutlined,
  SolutionOutlined,
  AuditOutlined
} from '@ant-design/icons';
import { Layout, Menu, theme, Button, Tag } from 'antd';

import EmployeeList from './components/EmployeeList';
import PayrollManager from './components/PayrollManager';
import LeaveManager from './components/LeaveManager';
import RecruitmentManager from './components/RecruitmentManager';
import AttendanceManager from './components/AttendanceManager';
import ObjectiveManager from './components/ObjectiveManager';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import PublicJobPortal from './components/PublicJobPortal';
import { getCurrentUser } from './api';

const { Header, Content, Footer, Sider } = Layout;

const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKey, setSelectedKey] = useState('dashboard');
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    if (isAuthenticated) {
      getCurrentUser()
        .then(res => {
          setUser(res.data);
          // Redirection intelligente selon le rôle
          if (res.data.role === 'CANDIDAT') setSelectedKey('recruitment');
          else if (res.data.role === 'AUDITEUR') setSelectedKey('dashboard');
          else if (res.data.role === 'EMPLOYE') setSelectedKey('leaves');
          else setSelectedKey('dashboard');
        })
        .catch(() => handleLogout());
    }
  }, [isAuthenticated]);

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  if (window.location.pathname === '/jobs') {
    return <PublicJobPortal />;
  }

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    setIsAuthenticated(false);
    setUser(null);
  };

  const getMenuItems = () => {
    if (!user) return [];
    
    const role = user.role;
    const allItems = [
      { key: 'dashboard', icon: <PieChartOutlined />, label: 'Tableau de Bord', roles: ['ADMIN', 'RH', 'MANAGER', 'AUDITEUR'] },
      { key: 'employees', icon: <TeamOutlined />, label: 'Personnel', roles: ['ADMIN', 'RH', 'AUDITEUR'] },
      { key: 'payroll', icon: <DollarCircleOutlined />, label: 'Paie & Frais', roles: ['ADMIN', 'RH', 'MANAGER', 'EMPLOYE', 'AUDITEUR'] },
      { key: 'leaves', icon: <CalendarOutlined />, label: 'Congés', roles: ['ADMIN', 'RH', 'MANAGER', 'EMPLOYE'] },
      { key: 'objectifs', icon: <CheckCircleOutlined />, label: 'Objectifs', roles: ['ADMIN', 'RH', 'MANAGER', 'EMPLOYE'] },
      { key: 'pointage', icon: <CheckCircleOutlined />, label: 'Pointage', roles: ['ADMIN', 'RH', 'EMPLOYE'] },
      { key: 'recruitment', icon: <SolutionOutlined />, label: 'Recrutement', roles: ['ADMIN', 'RH', 'CANDIDAT'] },
    ];

    return allItems
      .filter(item => item.roles.includes(role))
      .map(({ roles, ...rest }) => rest);
  };

  const renderContent = () => {
    switch (selectedKey) {
      case 'employees': return <EmployeeList />;
      case 'payroll': return <PayrollManager />;
      case 'leaves': return <LeaveManager />;
      case 'recruitment': return <RecruitmentManager />;
      case 'pointage': return <AttendanceManager />;
      case 'objectifs': return <ObjectiveManager />;
      case 'dashboard':
      default: return <Dashboard />;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold', fontSize: '12px' }}>
            SGRH AFRIQUE
        </div>
        <Menu 
          theme="dark" 
          mode="inline"
          selectedKeys={[selectedKey]}
          onClick={(e) => setSelectedKey(e.key)}
          items={getMenuItems()}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: '0 24px', background: colorBgContainer, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              {user && <Tag color="blue">{user.role} : {user.nom} {user.prenom}</Tag>}
            </div>
            <Button icon={<LogoutOutlined />} onClick={handleLogout}>Déconnexion</Button>
        </Header>
        <Content style={{ margin: '16px' }}>
          {renderContent()}
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          SGRH Afrique de l'Ouest ©{new Date().getFullYear()} - Système Certifié OHADA
        </Footer>
      </Layout>
    </Layout>
  );
};

export default App;
