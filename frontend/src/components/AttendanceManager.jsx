import React, { useEffect, useState } from 'react';
import { Card, Table, Tag, Typography, message } from 'antd';
import { getPointages } from '../api';

const { Title } = Typography;

const AttendanceManager = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPointages()
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(() => {
        message.error("Erreur lors du chargement des pointages");
        setLoading(false);
      });
  }, []);

  const columns = [
    { title: 'Date', dataIndex: 'date', key: 'date' },
    { title: 'Arrivée', dataIndex: 'heure_arrivee', key: 'heure_arrivee' },
    { title: 'Départ', dataIndex: 'heure_depart', key: 'heure_depart' },
    { title: 'Statut', dataIndex: 'statut', key: 'statut', render: (s) => <Tag color={s === 'PRESENT' ? 'green' : 'orange'}>{s}</Tag> },
  ];

  return (
    <Card>
      <Title level={3}>Gestion du Pointage (Temps & Présence)</Title>
      <Table dataSource={data} columns={columns} rowKey="id" loading={loading} />
    </Card>
  );
};

export default AttendanceManager;
