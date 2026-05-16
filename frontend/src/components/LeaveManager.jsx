import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Card, Modal, Form, Select, DatePicker, message, Tag, Tabs, Calendar, Badge } from 'antd';
import { CalendarOutlined, UnorderedListOutlined } from '@ant-design/icons';
import { getDemandesConge, getTypesConge, getEmployes, creerDemandeConge, getCurrentUser } from '../api';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;

const LeaveManager = () => {
  const [demandes, setDemandes] = useState([]);
  const [types, setTypes] = useState([]);
  const [employes, setEmployes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  const loadData = async () => {
    setLoading(true);
    try {
      const [demRes, typeRes, empRes, userRes] = await Promise.all([
        getDemandesConge(), 
        getTypesConge(), 
        getEmployes(),
        getCurrentUser()
      ]);
      const currentUser = userRes.data;
      setUser(currentUser);
      
      if (currentUser.role === 'EMPLOYE') {
        setDemandes(demRes.data.filter(d => d.employe === currentUser.id));
      } else {
        setDemandes(demRes.data);
      }
      setTypes(typeRes.data);
      setEmployes(empRes.data);
    } catch (err) {
      message.error("Erreur de chargement");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = (values) => {
    const { dates, ...rest } = values;
    const data = {
        ...rest,
        date_debut: dates[0].format('YYYY-MM-DD'),
        date_fin: dates[1].format('YYYY-MM-DD'),
        statut: 'EN_ATTENTE'
    };
    
    creerDemandeConge(data)
      .then(() => {
        message.success("Demande envoyée !");
        setIsModalOpen(false);
        loadData();
      })
      .catch(() => message.error("Erreur lors de l'envoi"));
  };

  const columns = [
    { title: 'Employé', dataIndex: 'employe_nom', key: 'nom' },
    { title: 'Type', dataIndex: 'type_conge_libelle', key: 'type' },
    { title: 'Début', dataIndex: 'date_debut', key: 'debut' },
    { title: 'Fin', dataIndex: 'date_fin', key: 'fin' },
    { 
        title: 'Statut', 
        dataIndex: 'statut', 
        key: 'statut',
        render: (s) => (
            <Tag color={s === 'APPROUVE' ? 'green' : s === 'REJETE' ? 'red' : 'gold'}>
                {s}
            </Tag>
        )
    },
    {
      title: 'Actions',
      key: 'action',
      render: (_, record) => (
        user?.role !== 'EMPLOYE' && (
          <Space size="middle">
            <Button type="link">Approuver</Button>
            <Button type="link" danger>Rejeter</Button>
          </Space>
        )
      ),
    },
  ];

  const dateCellRender = (value) => {
    const stringValue = value.format('YYYY-MM-DD');
    const listData = demandes.filter(d => 
        dayjs(stringValue).isAfter(dayjs(d.date_debut).subtract(1, 'day')) && 
        dayjs(stringValue).isBefore(dayjs(d.date_fin).add(1, 'day'))
    );
    return (
      <ul className="events">
        {listData.map((item) => (
          <li key={item.id}>
            <Badge status="warning" text={item.employe_nom} />
          </li>
        ))}
      </ul>
    );
  };

  return (
    <Card 
        title="Gestion des Congés" 
        extra={<Button type="primary" onClick={() => setIsModalOpen(true)}>Nouvelle Demande</Button>}
    >
      <Tabs defaultActiveKey="1">
        <Tabs.TabPane tab={<span><UnorderedListOutlined /> Liste</span>} key="1">
          <Table columns={columns} dataSource={demandes} rowKey="id" loading={loading} />
        </Tabs.TabPane>
        <Tabs.TabPane tab={<span><CalendarOutlined /> Calendrier</span>} key="2">
          <Calendar cellRender={dateCellRender} />
        </Tabs.TabPane>
      </Tabs>

      <Modal title="Soumettre une demande de congé" open={isModalOpen} onCancel={() => setIsModalOpen(false)} onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="employe" label="Employé" rules={[{ required: true }]}>
            <Select>
              {employes.map(e => <Select.Option key={e.id} value={e.id}>{e.prenom} {e.nom}</Select.Option>)}
            </Select>
          </Form.Item>
          <Form.Item name="type_conge" label="Type de congé" rules={[{ required: true }]}>
            <Select>
              {types.map(t => <Select.Option key={t.id} value={t.id}>{t.libelle}</Select.Option>)}
            </Select>
          </Form.Item>
          <Form.Item name="dates" label="Période" rules={[{ required: true }]}>
            <RangePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="motif" label="Motif">
            <Form.Item name="motif"><textarea style={{ width: '100%', borderRadius: '4px', border: '1px solid #d9d9d9', padding: '8px' }} rows={3} /></Form.Item>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default LeaveManager;
