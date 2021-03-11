import React, { useState, useEffect } from 'react';
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
    width: '100%',
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

const ArtistSearch = ({ onArtistSelect }) => {
  const [ searchTerm, setSearchTerm ] = useState('');
  const [ open, setOpen ] = React.useState(false);
  const [ options, setOptions ] = React.useState([]);
  const [ selectedArtist, setSelectedArtist ] = React.useState(null);
  const loading = searchTerm.length > 0 && open && options.length === 0;

  const classes = makeStyles(styles);

  const handleSearchChange = event => {
    setSearchTerm(event.target.value);
  };

  const handleSelectArtist = (event, value) => {
    if (typeof(value) !== 'string') {
      setSelectedArtist(value);
      setOpen(false);
      setOptions([]);
    }
  };

  useEffect(() => {
    if (selectedArtist) {
      if (onArtistSelect) {
        onArtistSelect(selectedArtist);
      }
      setSelectedArtist(null);
      setOpen(false);
      setOptions([]);
    }
  }, [ selectedArtist ]);

  const handleSearchKeyPress = async (event) => {
    if (event.key == 'Enter') {
      if (searchTerm && searchTerm.length > 2) {
        setOpen(true);
        const artists = await searchArtist(searchTerm);
        setOptions(artists);
      }
    }
  };

  return (
    <Container className={classes.container} >
      <Autocomplete
        id="artist-search-autocomplete"
        clearOnEscape={false}
        clearOnBlur={false}
        openOnFocus={false}
        freeSolo
        fullWidth
        value={selectedArtist}
        onChange={handleSelectArtist}
        open={open}
        onInput={() => setOpen(false)}
        getOptionSelected={(option, value) => option.name === value.name}
        getOptionLabel={(option) => option.name || option}
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
            onKeyPress={handleSearchKeyPress}
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