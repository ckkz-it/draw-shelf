import React from 'react';
import { NavLink } from 'react-router-dom';
import { Menu } from 'semantic-ui-react';

import { useStores } from '../../hooks/user-stores';

const PageHeader: React.FC = () => {
  const { authStore } = useStores();

  const onLogout = () => {
    authStore.logout();
  };

  return (
    <Menu pointing secondary>
      <Menu.Item name="Shelf" as={NavLink} to="/shelf" />
      <Menu.Item name="Settings" as={NavLink} to="/settings" />
      <Menu.Menu position="right">
        <Menu.Item name="Logout" onClick={onLogout} />
      </Menu.Menu>
    </Menu>
  );
};

export default PageHeader;
