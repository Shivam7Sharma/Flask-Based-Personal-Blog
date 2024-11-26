import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import BlogPosts from './components/BlogPosts';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CreatePost from './components/CreatePost';
import Dashboard from './components/Dashboard';

const App = () => {
    const [token, setToken] = useState(null);

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/create-post" element={<CreatePost />} />
          <Route path="/posts" element={<BlogPosts />} />
          
            </Routes>
        </Router>
    );
};

export default App;
