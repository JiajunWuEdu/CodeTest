import * as React from 'react';
import axios from "axios";
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import DatasetTable from '../dataset/DatasetTable'
import ExperimentTable from '../experiment/ExperimentTable';
import ReplyAllIcon from '@mui/icons-material/ReplyAll';
import Title from '../tool/Title';
import { API_URL } from '../../config.js';
import { useParams, Link as RouterLink } from "react-router-dom";

function ProjectPage(props) {
    const { projectId } = useParams();
    const [projectName, SetProjectName] = React.useState('Untitled Project');

    React.useEffect(() => {
        const getProjectName = () => {
            axios
                .get(API_URL + "project/name?id=" + projectId)
                .then(response => {
                    if (response.data) {
                        SetProjectName(response.data.name);
                    }
                }, error => {
                    if (error.response.data.msg) alert(error.response.data.msg);
                    SetProjectName('Project Name not Fetched');
                });
        };
        getProjectName();
    }, [projectId]);

    return (
        <>
            <Title component="h1">{projectName} <Button component={RouterLink} size="small" variant="text" to="/"><ReplyAllIcon />Go Back</Button></Title>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                <DatasetTable projectId={projectId} />
            </Paper>
            <p></p>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                <ExperimentTable projectId={projectId} />
            </Paper>
        </>
    );
}


export default ProjectPage;
