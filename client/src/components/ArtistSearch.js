import React, { useState, useEffect, useRef } from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CircularProgress from '@material-ui/core/CircularProgress';

import { searchArtist } from '../http/data';

const styles = theme => ({
  container: {
    width: 600,
    minWidth: 400,
  },
  img: {
    width: 40,
    height: 'auto'
  },
});

const SearchResultsItem = withStyles({
  img: {
    width: 40,
    height: 'auto',
  },
  container: {
    width: 'auto',
    height: 60
  }
})(({ artist, ...props }) => {
  const { classes } = props;
  return (
    <Grid container className={classes.container} spacing={1} >
      <Grid item><img className={classes.img} src={artist.image} /></Grid>
      <Grid item>
        <Grid container>
          <Grid item style={{ width: '100%'}}><Typography variant="h5">{artist.name}</Typography></Grid>
          <Grid item><Typography variant="body1">{artist.description}</Typography></Grid>
        </Grid>
      </Grid>
    </Grid>
  );
});

const ArtistSearch = (props) => {
  const [ searchTerm, setSearchTerm ] = useState();
  const [open, setOpen] = React.useState(false);
  const [options, setOptions] = React.useState([]);
  const loading = searchTerm && open && options.length === 0;

  const classes = makeStyles(styles);

  const handleSearchChange = event => {
    setSearchTerm(event.target.value);
  };

  useEffect(() => {
    (async () => {
      if (searchTerm && searchTerm.length > 2) {
        const artists = await searchArtist(searchTerm);
        setOptions(artists);
      }
    })();
  }, [ searchTerm ]);

  return (
    <Container className={classes.container} maxWidth="sm">
      <Autocomplete
        id="artist-search-autocomplete"
        clearOnEscape={false}
        clearOnBlur={false}
        fullWidth
        open={open}
        onOpen={() => {
          setOpen(true);
        }}
        onClose={() => {
          setOpen(false);
        }}
        getOptionSelected={(option, value) => option.name === value.name}
        getOptionLabel={(option) => option.name}
        options={options}
        loading={loading}
        renderOption={(option) => (
          <SearchResultsItem className={classes.container} artist={option} />
        )}
        renderInput={(params) => (
          <TextField
            {...params}
            fullWidth
            value={searchTerm}
            onChange={handleSearchChange}
            label="Artist name"
            variant="outlined"
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <React.Fragment>
                  {loading ? <CircularProgress color="inherit" size={20} /> : null}
                  {params.InputProps.endAdornment}
                </React.Fragment>
              ),
            }}
          />
        )}
      />
    </Container>
  );
};

export default ArtistSearch;