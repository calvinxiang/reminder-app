export const subscribeUser = async () => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        try {
            const registration = await navigator.serviceWorker.ready;
            const publicKey = process.env.REACT_APP_VAPID_PUBLIC_KEY; // Use the VAPID public key from .env
            
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(publicKey),
            });

            // Send subscription to your backend to store it
            await fetch('http://127.0.0.1:8000/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(subscription),
            });

            console.log('User is subscribed');
        } catch (error) {
            console.error('Error subscribing user:', error);
        }
    } else {
        console.warn('Push messaging is not supported');
    }
};
