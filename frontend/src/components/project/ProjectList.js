import * as React from 'react';
import Paper from '@mui/material/Paper';
import ProjectTable from './ProjectTable';
import Title from '../tool/Title';

function ProjectList(props) {
  return (
    <>
      <Title component="h1">Homepage</Title>
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
        <ProjectTable />
      </Paper>
    </>
  );
}


export default ProjectList;
