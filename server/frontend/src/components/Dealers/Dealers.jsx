import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [originalDealers, setOriginalDealers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  let [states, setStates] = useState([]);

  let dealer_url = "/djangoapp/get_dealers";

  const get_dealers = async () => {
    const res = await fetch(dealer_url, { method: "GET" });
    const retobj = await res.json();
    
    if (retobj.status === 200 && Array.isArray(retobj.dealers)) {
      let all_dealers = retobj.dealers;
      let states = all_dealers.map(dealer => dealer.state);

      setStates([...new Set(states)]);
      setDealersList(all_dealers);
      setOriginalDealers(all_dealers);
    } else {
      console.error("Unexpected API response:", retobj);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  const handleInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);

    const filtered = originalDealers.filter(dealer =>
      typeof dealer.state === "string" && dealer.state.toLowerCase().includes(query.toLowerCase())
    );

    setDealersList(filtered);
  };

  const handleLostFocus = () => {
    if (!searchQuery.trim()) {
      setDealersList(originalDealers);
    }
  };

  let isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header />
      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <input 
                type="text" 
                placeholder="Search states..." 
                onChange={handleInputChange} 
                onBlur={handleLostFocus} 
                value={searchQuery} 
              />
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {Array.isArray(dealersList) && dealersList.length > 0 ? (
            dealersList.map(dealer => (
              <tr key={dealer.id}>
                <td>{dealer.id ?? "N/A"}</td>
                <td><a href={`/dealer/${dealer.id}`}>{dealer.full_name ?? "Unknown"}</a></td>
                <td>{dealer.city ?? "Unknown"}</td>
                <td>{dealer.address ?? "No Address"}</td>
                <td>{dealer.zip ?? "00000"}</td>
                <td>{typeof dealer.state === "string" ? dealer.state : "Unknown"}</td>
                {isLoggedIn && (
                  <td>
                    <a href={`/postreview/${dealer.id}`}>
                      <img src={review_icon} className="review_icon" alt="Post Review" />
                    </a>
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr><td colSpan="6">No dealers found</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;
