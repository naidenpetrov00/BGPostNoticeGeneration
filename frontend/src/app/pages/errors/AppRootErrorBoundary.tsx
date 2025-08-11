import { useRouteError } from 'react-router-dom';

export const AppRootErrorBoundary = () => {
  const error = useRouteError() as any;
  const data = JSON.parse(error.data);

  return (
    <div role="alert" aria-live="assertive" aria-labelledby="error-message">
      <h1 id="error-message">{error.status}</h1>
      <h2>{data.sorry}</h2>
      <p>
        If you believe this is a mistake, please reach out to{' '}
        <a
          href="mailto:e.videnov@smart-projects.bg"
          aria-label="Email Emanuil Videnov"
        >
          e.videnov@smart-projects.bg
        </a>
        .
      </p>
    </div>
  );
};
