import React from 'react';
import { Link } from 'react-router-dom';
import { Menu } from 'semantic-ui-react';
import { observer } from 'mobx-react-lite';

import { useStores } from '../../hooks/user-stores';

const PageHeader: React.FC = observer(() => {
  const { authStore, userStore } = useStores();

  const onLogout = () => {
    authStore.logout();
  };

  return (
    <Menu pointing secondary>
      <Menu.Item name="Shelf" active as={Link} to="/shelf" />
      <Menu.Item name="Settings" as={Link} to="/settings" />
      <Menu.Menu position="right">
        <Menu.Item name={userStore.user!.name} />
        <Menu.Item name="Logout" onClick={onLogout} />
      </Menu.Menu>
    </Menu>
  );
});

export default PageHeader;
