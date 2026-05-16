export function useNotification() {
  const requestPermission = () => Notification.requestPermission();

  const notify = (title: string, body?: string) => {
    if (Notification.permission === 'granted') {
      new Notification(title, { body, icon: '/favicon.ico' });
    }
  };

  return { requestPermission, notify, permission: Notification.permission };
}
