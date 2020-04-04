import React, { ChangeEvent, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Button, Divider, Form, InputOnChangeData } from 'semantic-ui-react';

import AuthWrapper from '../Wrapper';
import { useStores } from '../../../hooks/user-stores';

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
      <Form onSubmit={onSubmit}>
        <Form.Input
          name="email"
          label="Email"
          type="email"
          value={form.email}
          onChange={handleChange}
        />
        <Form.Input
          name="password"
          label="Password"
          type="password"
          value={form.password}
          onChange={handleChange}
        />
        <div style={{ position: 'relative' }}>
          <Button type="submit">Submit</Button>
          <Divider vertical>Or</Divider>
          <Button as={Link} to="/sign-up" floated="right">
            Sign Up
          </Button>
        </div>
      </Form>
    </AuthWrapper>
  );
});

export default Login;
