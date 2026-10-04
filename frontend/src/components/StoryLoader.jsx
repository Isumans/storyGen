import {useState,useEffect} from 'react'
import {useParams, useNavigate} from 'react-router-dom'
import axios from 'axios'
import LoadingStatus from './LoadingStatus'
import StoryGame from './StoryGame'
import { API_BASE_URL } from '../util.js';

function StoryLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [story, setStory] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        loadStory(id);
    }, [id]);
    
    const loadStory = async (storyId) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            setStory(response.data);
            setLoading(false);
        } catch (err) {
            if (err.response && err.response.status === 404) {
                setError('Story not found.');
            }else{
                setError('Failed to load story. Please try again later.');
            } 
        }finally {
            setLoading(false);
        }
        
    }
    const createNewStory = async () => {
        navigate('/');
    }
    if (loading) { 
        return <LoadingStatus theme={"story"} />;
    }

    if (error) {
        return <div className="story-loader">
            <div className="error-message">
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}>Create New Story</button>
            </div>
        </div>
    }
    if (story) {
        return <div className="story-loader">
            <StoryGame story={story} onNewStory={createNewStory}/>
        </div>
    }

}
export default StoryLoader;