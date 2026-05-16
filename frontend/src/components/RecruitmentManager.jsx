import React, { useEffect, useState } from 'react';
import { Table, Button, Card, Tabs, Tag, Space, Select, message } from 'antd';
import { getOffres, getCandidatures, updateCandidature } from '../api';

const RecruitmentManager = () => {
  const [offres, setOffres] = useState([]);
  const [candidatures, setCandidatures] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = () => {
    setLoading(true);
    Promise.all([getOffres(), getCandidatures()])
      .then(([offRes, canRes]) => {
        setOffres(offRes.data);
        setCandidatures(canRes.data);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStatusChange = (id, newStatus) => {
    updateCandidature(id, { statut: newStatus })
      .then(() => {
        message.success("Statut mis à jour");
        loadData();
      });
  };

  const columnsCandidatures = [
    { title: 'Candidat', render: (_, r) => `${r.candidat_prenom} ${r.candidat_nom}` },
    { title: 'Offre', dataIndex: 'offre_titre', key: 'offre' },
    { 
        title: 'Statut', 
        dataIndex: 'statut', 
        key: 'statut',
        render: (s, record) => (
            <Select 
                defaultValue={s} 
                style={{ width: 120 }} 
                onChange={(v) => handleStatusChange(record.id, v)}
            >
                <Select.Option value="NOUVEAU">Nouveau</Select.Option>
                <Select.Option value="ENTRETIEN">Entretien</Select.Option>
                <Select.Option value="OFFRE">Offre</Select.Option>
                <Select.Option value="EMBAUCHE">Embauché</Select.Option>
                <Select.Option value="REJETE">Rejeté</Select.Option>
            </Select>
        )
    },
    { title: 'Date', dataIndex: 'date_postulation', key: 'date', render: (d) => new Date(d).toLocaleDateString() },
  ];

  return (
    <Card title="Gestion du Recrutement (ATS)">
      <Tabs defaultActiveKey="1">
        <Tabs.TabPane tab="Candidatures" key="1">
          <Table columns={columnsCandidatures} dataSource={candidatures} rowKey="id" loading={loading} />
        </Tabs.TabPane>
        <Tabs.TabPane tab="Offres d'Emploi" key="2">
          <Table 
            columns={[{ title: 'Titre', dataIndex: 'titre' }, { title: 'Date', dataIndex: 'date_publication' }]} 
            dataSource={offres} 
            rowKey="id" 
          />
        </Tabs.TabPane>
      </Tabs>
    </Card>
  );
};

export default RecruitmentManager;
