import React, { useState } from 'react';
import { createPost } from '../api';

const CreatePost = ({ token, setPosts }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleCreatePost = async (e) => {
        e.preventDefault();
        try {
            const response = await createPost({ title, content }, token);
            console.log('Post created:', response.data);

            // Fetch updated posts
            setPosts((prevPosts) => [
                ...prevPosts,
                { title, content, date_posted: new Date().toISOString(), id: Math.random() }, // Placeholder ID
            ]);
            setTitle('');
            setContent('');
        } catch (error) {
            console.error('Error creating post:', error.response?.data || error.message);
        }
    };

    return (
        <form onSubmit={handleCreatePost}>
            <input
                type="text"
                placeholder="Post Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <textarea
                placeholder="Post Content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
            ></textarea>
            <button type="submit">Create Post</button>
        </form>
    );
};

export default CreatePost;
