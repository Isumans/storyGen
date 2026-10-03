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

    