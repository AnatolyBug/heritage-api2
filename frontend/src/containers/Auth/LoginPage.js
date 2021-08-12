import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";

// @material-ui/icons
import Email from "@material-ui/icons/Email";
// import IconButton from '@material-ui/core/IconButton';
// import Input from '@material-ui/core/Input';
// import FilledInput from '@material-ui/core/FilledInput';
// import OutlinedInput from '@material-ui/core/OutlinedInput';
// import InputLabel from '@material-ui/core/InputLabel';
// import FormHelperText from '@material-ui/core/FormHelperText';
// import FormControl from '@material-ui/core/FormControl';
// import TextField from '@material-ui/core/TextField';
// import Visibility from '@material-ui/icons/Visibility';
// import VisibilityOff from '@material-ui/icons/VisibilityOff';

import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import CardFooter from "components/Card/CardFooter.js";

import styles from "assets/jss/material-dashboard-pro-react/views/loginPageStyle.js";
const useStyles = makeStyles(styles);

import { login } from "redux/actions/auth";

const LoginPage = (props) => {
  const classes = useStyles();
  const [cardAnimation, setCardAnimation] = useState("cardHidden");

  useEffect(() => {
    let id = setTimeout(function() {
      setCardAnimation("");
    }, 700);
    return function cleanup() {
      window.clearTimeout(id);
    };
  });

  // handleChangeInput = e => {
  //   let errors = this.state.errors;
  //   if (errors[e.target.name] !== '') {
  //     errors[e.target.name] = '';
  //     this.setState(errors);
  //   }
  // };

  if (props.isAuthenticated) {
    return (
      <Redirect to='/dashboard'/>
    )
  } else {
    return (
      <div className={classes.container}>
        <GridContainer justify="center">
          <GridItem xs={12} sm={6} md={4}>
            <form>
              <Card login className={classes[cardAnimation]}>
                <CardHeader
                  className={`${classes.cardHeader} ${classes.textCenter}`}
                  color="rose"
                >
                  <h4 className={classes.cardTitle}>Log in</h4>
                  {/*<div className={classes.socialLine}>*/}
                  {/*  {[*/}
                  {/*    "fab fa-facebook-square",*/}
                  {/*    "fab fa-twitter",*/}
                  {/*    "fab fa-google-plus"*/}
                  {/*  ].map((prop, key) => {*/}
                  {/*    return (*/}
                  {/*      <Button*/}
                  {/*        color="transparent"*/}
                  {/*        justIcon*/}
                  {/*        key={key}*/}
                  {/*        className={classes.customButtonClass}*/}
                  {/*      >*/}
                  {/*        <i className={prop} />*/}
                  {/*      </Button>*/}
                  {/*    );*/}
                  {/*  })}*/}
                  {/*</div>*/}
                </CardHeader>
                <CardBody>
                  <CustomInput
                    labelText="Email..."
                    id="email"
                    formControlProps={{
                      fullWidth: true
                    }}
                    inputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <Email className={classes.inputAdornmentIcon} />
                        </InputAdornment>
                      )
                    }}
                  />
                  <CustomInput
                    labelText="Password"
                    id="password"
                    formControlProps={{
                      fullWidth: true
                    }}
                    inputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <Icon className={classes.inputAdornmentIcon}>
                            lock_outline
                          </Icon>
                        </InputAdornment>
                      ),
                      type: "password",
                      autoComplete: "off"
                    }}
                  />
                </CardBody>
                <CardFooter className={classes.justifyContentCenter}>
                  <row>
                  <Button color="rose" simple size="lg" block>
                    Let&apos; s Go
                  </Button>
                  </row>
                  <row>
                  <span>Don&apos;t you have an account? </span>
                  <a href="/register">Join</a>
                  </row>
                </CardFooter>
              </Card>
            </form>
          </GridItem>
        </GridContainer>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch) => ({
  login: (email, password) => dispatch(login(email, password)),
});

export default connect(mapStateToProps, mapDispatchToProps)(LoginPage);
