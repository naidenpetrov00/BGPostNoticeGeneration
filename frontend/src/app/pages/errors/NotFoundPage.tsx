import { Link } from 'react-router-dom';
import { paths } from '../../../config/paths';

export const NotFoundRoute = () => {
  return (
    <div
      className="mt-52 flex flex-col items-center font-semibold"
      role="alert"
      aria-live="assertive"
    >
      <h1 id="not-found-heading">404 - Page Not Found</h1>
      <p>
        Sorry, the page you are looking for does not exist or may have been
        moved. Please check the URL or go back to the home page.
      </p>
      <Link to={paths.home.path} replace aria-label="Go back to the home page">
        Go to Home
      </Link>
    </div>
  );
};
