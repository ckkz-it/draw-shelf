import React, { ChangeEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Button, Divider, Form, InputOnChangeData } from 'semantic-ui-react';

import AuthWrapper from '../Wrapper';
import { useStores } from '../../../hooks/user-stores';
import { ISignUp } from '../../../interfaces/auth';

const Register: React.FC = observer(() => {
  const [form, setForm] = useState<ISignUp>({ name: '', phone: '', email: '', password: '' });

  const { authStore } = useStores();

  const handleChange = (e: ChangeEvent, { name, value }: InputOnChangeData) => {
    setForm((v) => ({ ...v, [name]: value }));
  };

  const onSubmit = async () => {
    await authStore.signUp(form);
  };

  return (
    <AuthWrapper>
      <Form onSubmit={onSubmit}>
        <Form.Input
          name="name"
          label="Name"
          type="text"
          value={form.name}
          onChange={handleChange}
        />
        <Form.Input
          name="email"
          label="Email"
          type="email"
          value={form.email}
          onChange={handleChange}
        />
        <Form.Input
          name="phone"
          label="Phone"
          type="text"
          value={form.phone}
          onChange={handleChange}
        />
        <Form.Input
          name="password"
          label="Password"
          type="password"
          value={form.password}
          onChange={handleChange}
        />
        <div className="position-relative">
          <Button type="submit">Submit</Button>
          <Divider vertical>Or</Divider>
          <Button as={Link} to="/login" floated="right">
            Login
          </Button>
        </div>
      </Form>
    </AuthWrapper>
  );
});

export default Register;
