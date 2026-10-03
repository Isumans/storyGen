import {useState, useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import axios from 'axios';
import ThemeInput from './ThemeInput';
import LoadingStatus from './LoadingStatus';
import { API_BASE_URL } from '../util.js';

function StoryGenerator() {
    const navigate = useNavigate()
    const [Theme, setTheme] = useState('');
    const [jobId, setJobId] = useState(null);
    const [jobStatus, setJobStatus] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);


    useEffect(() => {
        let pullInterval;

        if (jobId && (jobStatus === 'pending' || jobStatus === 'in_progress')) {
            pullInterval = setInterval(() => {
                pullJobStatus(jobId);
            }, 5000);
        }
        return () => {
            if (pullInterval) {
                clearInterval(pullInterval);
            }
        };

    }, [jobId, jobStatus]);

    const generateStory = async (theme) => {
        setLoading(true);
        setError(null);
        setTheme(theme);
        try {
            const response = await axios.post(`${API_BASE_URL}/stories/create`, {theme});
            const {job_id, status} = response.data;
            setJobId(job_id);
            setJobStatus(status);

            pullJobStatus(job_id);
        } catch (error) {
            setError('Failed to generate the story: ${error.message}');
            setLoading(false);
        }
    }
    const pullJobStatus = async (id) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/jobs/${id}`);
            const {status, story_id, error: jobError} = response.data;
            setJobStatus(status);
            if (status === 'completed' && story_id) {
                fetchStory(story_id);
            }else if (status === 'failed') {
                setError(jobError || 'Story generation failed. Please try again.');
                setLoading(false);
            }
        } catch (err) {
            if (err.response?.status === 404) {
                setError('Job not found. Please try again.');
                setLoading(false);
            }
        }
    };

    const fetchStory = async (id) => {
        try {
            setLoading(false);
            setJobStatus('completed');
            navigate(`/story/${id}`);
        } catch (err) {
            setError('Failed to fetch the story. {err.message}');
            setLoading(false);
        }
    };

    const reset = () => {
        setTheme('');
        setJobId(null);
        setJobStatus(null);
        setError(null);
        setLoading(false);
    }

    return <div className="story-generator">
        {error && <div className="error-message">
            <p>{error}</p>
            <button onClick={reset}>Try Again</button>
        </div>}
    
    {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory} />}
    {loading && <LoadingStatus theme={Theme} />}
    </div>

}

export default StoryGenerator;