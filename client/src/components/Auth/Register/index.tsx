import React, { ChangeEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { Button, Form, InputOnChangeData } from 'semantic-ui-react';

import AuthWrapper from '../AuthWrapper';
import { useStores } from '../../../hooks/use-stores';
import { ISignUp } from '../../../interfaces/auth';
import { StyledButtonWrapper } from '../styles';
import AuthHeader from '../AuthHeader';

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
      <AuthHeader>Register</AuthHeader>
      <Form onSubmit={onSubmit}>
        <Form.Input
          name="name"
          placeholder="Name"
          size="large"
          type="text"
          value={form.name}
          onChange={handleChange}
        />
        <Form.Input
          name="email"
          placeholder="Email"
          size="large"
          type="email"
          value={form.email}
          onChange={handleChange}
        />
        <Form.Input
          name="phone"
          placeholder="Phone"
          size="large"
          type="text"
          value={form.phone}
          onChange={handleChange}
        />
        <Form.Input
          name="password"
          placeholder="Password"
          size="large"
          type="password"
          value={form.password}
          onChange={handleChange}
        />
        <StyledButtonWrapper>
          <Button type="submit" color="yellow">
            Sign Up
          </Button>
          <Button inverted color="orange" type="button" as={Link} to="/login" floated="right">
            Login
          </Button>
        </StyledButtonWrapper>
      </Form>
    </AuthWrapper>
  );
});

export default Register;
