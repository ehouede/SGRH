import React, { useEffect, useState } from 'react';
import { Card, List, Button, Typography, Row, Col, Tag } from 'antd';
import { getPublicOffres } from '../api';

const { Title, Paragraph } = Typography;

const PublicJobPortal = () => {
  const [offres, setOffres] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPublicOffres()
      .then(res => {
        setOffres(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: '50px', background: '#f0f2f5', minHeight: '100vh' }}>
      <Row justify="center">
        <Col span={16}>
          <Title level={2} style={{ textAlign: 'center', marginBottom: '40px' }}>
            Portail de Recrutement - SGRH AFRIQUE
          </Title>
          <List
            loading={loading}
            dataSource={offres}
            renderItem={item => (
              <Card style={{ marginBottom: '20px' }}>
                <Title level={4}>{item.titre}</Title>
                <Tag color="blue">Publié le {item.date_publication}</Tag>
                <Paragraph ellipsis={{ rows: 2 }}>{item.description}</Paragraph>
                <Button type="primary">Postuler maintenant</Button>
              </Card>
            )}
          />
        </Col>
      </Row>
    </div>
  );
};

export default PublicJobPortal;
