import React, { Component } from 'react'
import { Link } from "react-router-dom"
import "./css/NavBar.css"
import logo from './images/OpenAi.png'

export class Navbar extends Component {
  render() {
    return (
      <header className='header'>
        <img src={logo} alt="logo"/>
        <nav className="navbar"> 
          <ul className="navbar-nav">
              <li className="nav-item">
                  <Link to="/" className="nav-link">HomePage</Link>
              </li>
              <li className="nav-item">
                  <Link to="/textgen" className="nav-link">Text generation</Link>
              </li>
              <li className="nav-item">
                  <Link to="/imagegen" className="nav-link">Image generation</Link>
              </li>
              <li className="nav-item">
                  <Link to="/voicegen" className="nav-link">Voice generation</Link>
              </li>
              <li className="nav-item">
                  <Link to="/videogen" className="nav-link">Video generation</Link>
              </li>
          </ul>
        </nav>
      </header>
      
    )
  }
}

export default Navbar
