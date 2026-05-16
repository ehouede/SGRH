import React from 'react';
import { Form, Input, Button, Card, message, Row, Col } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { login } from '../api';

const Login = ({ onLoginSuccess }) => {
  const onFinish = (values) => {
    login(values.username, values.password)
      .then(res => {
        localStorage.setItem('token', res.data.access);
        localStorage.setItem('refresh', res.data.refresh);
        message.success("Connexion réussie !");
        onLoginSuccess();
      })
      .catch(() => {
        message.error("Identifiants incorrects");
      });
  };

  return (
    <div style={{ background: '#f0f2f5', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Card title="SGRH Afrique - Connexion" style={{ width: 400, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
        <Form name="login" onFinish={onFinish} layout="vertical">
          <Form.Item name="username" rules={[{ required: true, message: 'Veuillez saisir votre utilisateur' }]}>
            <Input prefix={<UserOutlined />} placeholder="Utilisateur (admin)" size="large" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: 'Veuillez saisir votre mot de passe' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="Mot de passe (admin123)" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" style={{ width: '100%' }} size="large">
              Se connecter
            </Button>
          </Form.Item>
          <div style={{ textAlign: 'center' }}>
            <Button type="link" onClick={() => window.location.href = '/jobs'}>
              Voir les offres d'emploi (Candidats)
            </Button>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Login;
