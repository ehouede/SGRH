import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Card, Modal, Form, Select, DatePicker, message, Tag } from 'antd';
import { getEmployes, genererPaie, getBulletins, getBulletinPdfUrl, getCurrentUser } from '../api';
import dayjs from 'dayjs';
import { FilePdfOutlined } from '@ant-design/icons';

const PayrollManager = () => {
  const [bulletins, setBulletins] = useState([]);
  const [employes, setEmployes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [form] = Form.useForm();

  const loadData = async () => {
    setLoading(true);
    try {
      const [bulRes, empRes, userRes] = await Promise.all([getBulletins(), getEmployes(), getCurrentUser()]);
      const currentUser = userRes.data;
      setUser(currentUser);
      
      if (currentUser.role === 'EMPLOYE') {
        setBulletins(bulRes.data.filter(b => b.employe === currentUser.id));
      } else {
        setBulletins(bulRes.data);
      }
      setEmployes(empRes.data);
    } catch (err) {
      message.error("Erreur de chargement des données");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGenerate = (values) => {
    const { employe_id, periode } = values;
    const formattedDate = periode.startOf('month').format('YYYY-MM-DD');
    
    genererPaie(employe_id, formattedDate)
      .then(() => {
        message.success("Bulletin généré avec succès !");
        setIsModalOpen(false);
        loadData();
      })
      .catch((err) => {
        message.error(err.response?.data?.error || "Erreur lors de la génération");
      });
  };

  const columns = [
    { title: 'Période', dataIndex: 'periode', key: 'periode', render: (t) => dayjs(t).format('MM/YYYY') },
    { title: 'Employé', key: 'employe', render: (_, r) => `${r.employe_prenom} ${r.employe_nom}` },
    { title: 'Salaire Brut', dataIndex: 'salaire_brut', key: 'brut', render: (v) => `${v} CFA` },
    { title: 'Salaire Net', dataIndex: 'salaire_net', key: 'net', render: (v) => <Tag color="green">{v} CFA</Tag> },
    {
      title: 'Actions',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            type="primary" 
            icon={<FilePdfOutlined />} 
            onClick={() => window.open(getBulletinPdfUrl(record.id), '_blank')}
          >
            PDF
          </Button>
          <Button type="link" danger>Supprimer</Button>
        </Space>
      ),
    },
  ];

  return (
    <Card 
        title="Gestion de la Paie" 
        extra={user?.role !== 'EMPLOYE' && <Button type="primary" onClick={() => setIsModalOpen(true)}>Générer Bulletin</Button>}
    >
      <Table columns={columns} dataSource={bulletins} rowKey="id" loading={loading} />

      <Modal title="Générer un nouveau bulletin" open={isModalOpen} onCancel={() => setIsModalOpen(false)} onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={handleGenerate}>
          <Form.Item name="employe_id" label="Employé" rules={[{ required: true }]}>
            <Select placeholder="Sélectionner un employé">
              {employes.map(emp => (
                <Select.Option key={emp.id} value={emp.id}>{emp.prenom} {emp.nom}</Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="periode" label="Mois" rules={[{ required: true }]}>
            <DatePicker picker="month" style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default PayrollManager;
