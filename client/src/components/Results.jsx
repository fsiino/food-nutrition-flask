import React from 'react';

const Results = ({ loadedFoods, isLoading, notFound, errors, fieldsets }) => {
  if (isLoading) {
    return (
      <h3>
        Loading...
      </h3>
    )
  } else if (loadedFoods.length) {
    return (
      <>
        <div className="header-grid-container">
          <div className="header-grid-food">Food</div>
          <div className="header-grid-nutrients">Nutrients</div>
        </div>  
        {loadedFoods}
      </>
    )
  } else if (notFound) {
    return (
      <h3>
        No results found.
      </h3>
    )
  } else {
    return (
      <>
        <h4 style={{ color: "red" }}>
          {errors}
        </h4>
        <h3>
          Results will display here.
        </h3>
      </>
    )
  }
}

export default Results;

