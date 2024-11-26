import React, { useEffect, useState } from 'react';
import { getPosts } from '../api';

const Dashboard = () => {
    const [posts, setPosts] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const posts = await getPosts();
                setPosts(posts);
            } catch (err) {
                setError('Failed to fetch posts.');
            }
        };
        fetchPosts();
    }, []);

    return (
        <div>
            <h2>Your Blog Posts</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <ul>
                {posts.map((post) => (
                    <li key={post.id}>
                        <h3>{post.title}</h3>
                        <p>{post.content}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Dashboard;
