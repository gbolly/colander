import "./styles.scss";

const Navbar = () => {
  return (
    <nav className="navBar navbar navbar-expand-lg">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">
          <img
            className='borderRadius-5'
            alt="twikkle"
            src={require('../../twinkle.png')}
            width="150"
            height="50"
          />
        </a>
        <button className="navbar-toggler" type="button">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
          </ul>
          <button
            className="signUpbtn btn d-flex text-white px-6 py-2 mr-2 mb-2 rounded"
            type="submit"
          >
            Sign Up
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
