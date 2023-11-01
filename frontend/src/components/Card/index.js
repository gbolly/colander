import React from "react";

import "./styles.scss";

const Card = ({ data }) => {
  let badgeColor =
  data.skills_score < 40
    ? "badge-light"
    : data.skills_score >= 40 && data.skills_score < 70
    ? "badge-warning3"
    : "badge-success textBlack";

  return (
    <div className="card border-0 candidateCard">
      <div className="position-relative">
        <div className="card-img-overlay three">
          <span className={`badge ${badgeColor} text-uppercase`}>{data.skills_score}% match</span>
        </div>
        <div className="card-smooth-caption">
          <div className="d-flex justify-content-between align-items-center">
            <div className="mr-auto">
              <h3 className="card-title textBlack text-uppercase">{data.names}</h3>
              <h6 className="card-subtitle textBlack">{data.email}</h6>
            </div>
          </div>
        </div>
      </div>
      <div className="card-body">
        <h6 className="font-weight-bold text-uppercase textBlack">Skills</h6>
        <p className=" textBlack card-text skills font-weight-light">
          {data.skills.length > 15 ? (
            <span>
              {data.skills.slice(0, 15).toString().split(',').join(', ')}
              ...
            </span>
            ) : (
              <span>{data.skills.toString()}</span>
          )}
        </p>
      </div>

      <div className="card-footer">
        <div className="media align-items-center">
          <div className="media-body"><a className="card-link text-primary read-more" href="/">Read More</a></div>
          <div className="footerright">
            <div className="tnlink3"><i className="fas fa-heart" aria-hidden="true"></i></div>
            <div className="tnlink3"><i className="fas fa-share-nodes" aria-hidden="true"></i></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card;
