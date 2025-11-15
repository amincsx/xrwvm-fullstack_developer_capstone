import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';


const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState();
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const navigate = useNavigate();
  let curr_url = window.location.href;
  let root_url = curr_url.substring(0,curr_url.indexOf("postreview"));
  let params = useParams();
  let id =params.id;
  let dealer_url = root_url+`djangoapp/dealer/${id}`;
  let review_url = root_url+`djangoapp/add_review`;
  let carmodels_url = root_url+`djangoapp/get_cars`;

  const postreview = async ()=>{
    try {
      let name = sessionStorage.getItem("firstname")+" "+sessionStorage.getItem("lastname");
      //If the first and second name are stores as null, use the username
      if(name.includes("null")) {
        name = sessionStorage.getItem("username");
      }
      
      console.log('PostReview - User:', name);
      console.log('PostReview - Form data:', { model, review, date, year });
      
      if(!model || review === "" || date === "" || year === "" || model === "") {
        alert("All details are mandatory")
        return;
      }

      let model_split = model.split(" ");
      let make_chosen = model_split[0];
      let model_chosen = model_split[1];

      let jsoninput = JSON.stringify({
        "name": name,
        "dealership": id,
        "review": review,
        "purchase": true,
        "purchase_date": date,
        "car_make": make_chosen,
        "car_model": model_chosen,
        "car_year": year,
      });

      console.log('PostReview - Sending data:', jsoninput);
      
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      console.log('PostReview - Response status:', res.status);
      const json = await res.json();
      console.log('PostReview - Response data:', json);
      
      if (json.status === 200) {
          alert("Review posted successfully!");
          navigate(`/dealer/${id}`);
      } else {
          alert("Error posting review: " + (json.message || "Unknown error"));
      }
    } catch (error) {
      console.error('Error in postreview:', error);
      alert("Error posting review: " + error.message);
    }
  }
  const get_dealer = async ()=>{
    try {
      const res = await fetch(dealer_url, {
        method: "GET"
      });
      const retobj = await res.json();
      console.log('PostReview - Dealer API response:', retobj);
      
      if(retobj.status === 200) {
        // The API returns a single dealer object, not an array
        setDealer(retobj.dealer)
      }
    } catch (error) {
      console.error('Error fetching dealer for PostReview:', error);
    }
  }

  const get_cars = async ()=>{
    try {
      const res = await fetch(carmodels_url, {
        method: "GET"
      });
      const retobj = await res.json();
      console.log('PostReview - Cars API response:', retobj);
      
      if(retobj.CarModels) {
        let carmodelsarr = Array.from(retobj.CarModels)
        setCarmodels(carmodelsarr)
      }
    } catch (error) {
      console.error('Error fetching cars for PostReview:', error);
    }
  }
  useEffect(() => {
    get_dealer();
    get_cars();
  },[]);


  return (
    <div>
      <Header/>
      <div  style={{margin:"5%"}}>
      <h1 style={{color:"darkblue"}}>{dealer.full_name}</h1>
      <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
      <div className='input_field'>
      Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)}/>
      </div>
      <div className='input_field'>
      Car Make 
      <select name="cars" id="cars" onChange={(e) => setModel(e.target.value)}>
      <option value="" selected disabled hidden>Choose Car Make and Model</option>
      {carmodels.map(carmodel => (
          <option value={carmodel.CarMake+" "+carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
      ))}
      </select>        
      </div >

      <div className='input_field'>
      Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015}/>
      </div>

      <div>
      <button className='postreview' onClick={postreview}>Post Review</button>
      </div>
    </div>
    </div>
  )
}
export default PostReview
