
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSession } from 'next-auth/react';

const withAuth = (WrappedComponent) => {
  return (props) => {
    const { data: session, status } = useSession();
    const router = useRouter();

    useEffect(() => {
      if (status === "unauthenticated") {
        router.replace('/login');
      }
    }, [status, router]);

    if (status === "authenticated") {
      return <WrappedComponent {...props} />;
    }

    return null; // Render nothing if not authenticated
  };
};

export default withAuth;
