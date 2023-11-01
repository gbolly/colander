const GradientBackground = ({ children }) => {
  const backgroundStyle = {
    background: 'linear-gradient(120deg, #F4FDFF, #c2e9fb9d)', // Customize the gradient colors
    width: '100vw',
    height: '100vh',
    position: 'fixed',
    top: 0,
    left: 0,
    zIndex: -1,
  };

  return (
    <div style={backgroundStyle}>{children}</div>
  );
};

export default GradientBackground;
