import React, { ChangeEvent, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Button, Form, Header, InputOnChangeData } from 'semantic-ui-react';

import AuthWrapper from '../Wrapper';
import { useStores } from '../../../hooks/user-stores';
import { StyledButtonWrapper } from './styles';

const Login: React.FC = observer(() => {
  const [form, setForm] = useState({ email: '', password: '' });

  const history = useHistory();
  const { authStore } = useStores();

  const handleChange = (e: ChangeEvent, { name, value }: InputOnChangeData) => {
    setForm((v) => ({ ...v, [name]: value }));
  };

  const onSubmit = async () => {
    const { email, password } = form;
    await authStore.login(email, password);
    history.push('/shelf');
  };

  return (
    <AuthWrapper>
      <Header as="h1" textAlign="center" color="grey" style={{ marginBottom: '2rem' }}>
        Login
      </Header>
      <Form onSubmit={onSubmit}>
        <Form.Input
          name="email"
          placeholder="Email"
          type="email"
          size="large"
          value={form.email}
          onChange={handleChange}
        />
        <Form.Input
          name="password"
          placeholder="Password"
          type="password"
          size="large"
          value={form.password}
          onChange={handleChange}
        />
        <StyledButtonWrapper>
          <Button type="submit" color="yellow">
            Login
          </Button>
          <Button inverted color="orange" as={Link} to="/sign-up">
            Sign Up
          </Button>
        </StyledButtonWrapper>
      </Form>
    </AuthWrapper>
  );
});

export default Login;
