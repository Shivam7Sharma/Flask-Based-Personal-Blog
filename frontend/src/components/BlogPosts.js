import React, { useEffect, useState } from 'react';
import { getPosts } from '../api';

const BlogPosts = () => {
    const [posts, setPosts] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const data = await getPosts();
                setPosts(data);
            } catch (err) {
                setError('Failed to fetch posts.');
            }
        };
        fetchPosts();
    }, []);

    if (error) return <div>{error}</div>;

    return (
        <div>
            <h2>Your Blog Posts</h2>
            {posts.length === 0 ? (
                <p>No posts available.</p>
            ) : (
                <ul>
                    {posts.map((post) => (
                        <li key={post.id}>
                            <h3>{post.title}</h3>
                            <p>{post.content}</p>
                            <small>{new Date(post.date_posted).toLocaleString()}</small>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default BlogPosts;
