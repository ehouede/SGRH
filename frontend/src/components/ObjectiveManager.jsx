import React, { useEffect, useState } from 'react';
import { Card, List, Progress, Typography, Tag, message, Spin } from 'antd';
import { getObjectifs } from '../api';

const { Title, Text } = Typography;

const ObjectiveManager = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getObjectifs()
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(() => {
        message.error("Erreur lors du chargement des objectifs");
        setLoading(false);
      });
  }, []);

  if (loading) return <Spin size="large" />;

  return (
    <Card title={<Title level={3}>Objectifs & Performance</Title>}>
      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              title={item.titre}
              description={<Text type="secondary">Echeance : {item.date_limite}</Text>}
            />
            <div style={{ width: 200, marginRight: 20 }}>
              <Progress percent={item.pourcentage_completion} size="small" />
            </div>
            <Tag color={item.pourcentage_completion === 100 ? 'green' : 'blue'}>
              {item.pourcentage_completion === 100 ? 'TERMINE' : 'EN_COURS'}
            </Tag>
          </List.Item>
        )}
      />
    </Card>
  );
};

export default ObjectiveManager;
