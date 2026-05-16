import React, { useEffect, useState } from 'react';
import { Table, Tag, Space, Card, Skeleton, message, Tabs, Tree, Button } from 'antd';
import { TeamOutlined, ApartmentOutlined, FileTextOutlined } from '@ant-design/icons';
import { getEmployes, getContratPdfUrl } from '../api';

const EmployeeList = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEmployes()
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        message.error("Erreur lors du chargement des employés");
        setLoading(false);
      });
  }, []);

  const columns = [
    {
      title: 'Matricule',
      dataIndex: 'matricule',
      key: 'matricule',
    },
    {
      title: 'Prénom',
      dataIndex: 'prenom',
      key: 'prenom',
    },
    {
      title: 'Nom',
      dataIndex: 'nom',
      key: 'nom',
    },
    {
      title: 'Poste',
      dataIndex: 'poste',
      key: 'poste',
    },
    {
      title: 'Service',
      dataIndex: 'service',
      key: 'service',
    },
    {
      title: 'Actions',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<FileTextOutlined />} 
            onClick={() => window.open(getContratPdfUrl(record.id), '_blank')}
          >
            Contrat
          </Button>
          <a style={{ color: 'red' }}>Supprimer</a>
        </Space>
      ),
    },
  ];

  const treeData = [
    {
      title: 'Directeur Général',
      key: '0-0',
      children: data.map(emp => ({
        title: `${emp.prenom} ${emp.nom} - ${emp.poste}`,
        key: emp.id,
      })),
    },
  ];

  return (
    <Card title="Gestion du Personnel" variant="outlined">
      <Tabs defaultActiveKey="1">
        <Tabs.TabPane tab={<span><TeamOutlined /> Liste</span>} key="1">
          {loading ? (
            <Skeleton active />
          ) : (
            <Table columns={columns} dataSource={data} rowKey="id" />
          )}
        </Tabs.TabPane>
        <Tabs.TabPane tab={<span><ApartmentOutlined /> Organigramme</span>} key="2">
          <div style={{ padding: '20px', background: '#fafafa', borderRadius: '8px' }}>
            <Tree
                showLine
                defaultExpandAll
                treeData={treeData}
            />
          </div>
        </Tabs.TabPane>
      </Tabs>
    </Card>
  );
};

export default EmployeeList;
