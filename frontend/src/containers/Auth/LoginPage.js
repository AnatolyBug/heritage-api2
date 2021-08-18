import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";
import { useHistory } from "react-router-dom";
import { toastr } from "react-redux-toastr";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from '@material-ui/core/IconButton';
import InputAdornment from '@material-ui/core/InputAdornment';
import FormHelperText from '@material-ui/core/FormHelperText';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import Email from "@material-ui/icons/Email";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import styles from "assets/jss/material-dashboard-pro-react/views/registerPageStyle";
import { login } from "redux/actions/auth";
import { validateEmail } from "helpers/commonHelper";
import CustomInput from "../../components/CustomInput/CustomInput";

const useStyles = makeStyles(styles);

const LoginPage = (props) => {
  const classes = useStyles();
  const history = useHistory();
  // const [cardAnimation, setCardAnimation] = useState("cardHidden");
  const [values, setValues] = useState({
    email: '',
    password: '',
    showPassword: false,
  });
  const [errorText, setErrorText] = useState({
    email: '',
    password: ''
  })

  // useEffect(() => {
  //   let id = setTimeout(function() {
  //     setCardAnimation("");
  //   }, 700);
  //   return function cleanup() {
  //     window.clearTimeout(id);
  //   };
  // });

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
    if (event.target.value !== '') {
      setErrorText({...errorText, [prop]: ''});
    }
  };

  const handleClickShowPassword = () => {
    setValues({ ...values, showPassword: !values.showPassword });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleLogin = e => {
    e.preventDefault();

    if (values.email === '') {
      setErrorText({...errorText, email: 'Email is required'});
      return;
    }

    if (!validateEmail(values.email)) {
      setErrorText({...errorText, email: 'Email is invalid'});
      return;
    }

    if (values.password === '') {
      setErrorText({...errorText, password: 'Password is required'});
      return;
    }

    props.login(values.email, values.password)
      .then(res => {
        console.log(res)
      })
      .catch((err) => {
        console.log(err.response.data.non_field_errors[0])
        if (err.response.data.non_field_errors[0] === 'email_verification') {
          toastr.warning('Warning!', 'Please verify your email address.')
          history.push('/login/email_verification')
        } else {
          toastr.error('Fail!', 'Please check your email and password.')
        }
      })
  };

  if (props.isAuthenticated) {
    return (
      <Redirect to='/dashboard'/>
    )
  } else {
    return (
      <div className={classes.container}>
        <GridContainer justify="center">
          <GridItem xs={12} sm={12} md={5}>
            <Card className={classes.cardSignup}>
              <h2 className={classes.cardTitle}>Log in</h2>
              <CardBody>
                <GridContainer justify="center">
                  <GridItem xs={12} sm={8} md={10}>
                    <form className={classes.form}>
                      <CustomInput
                        formControlProps={{
                          fullWidth: true,
                          className: classes.customFormControlClasses
                        }}
                        value={values.email}
                        onChange={handleChange('email')}
                        inputProps={{
                          startAdornment: (
                            <InputAdornment
                              position="start"
                              className={classes.inputAdornment}
                            >
                              <IconButton aria-label="email">
                                <Email className={classes.inputAdornmentIcon} />
                              </IconButton>
                            </InputAdornment>
                          ),
                          placeholder: "Email..."
                        }}
                      />
                      <FormHelperText error>{errorText.email}</FormHelperText>
                      <CustomInput
                        formControlProps={{
                          fullWidth: true,
                          className: classes.customFormControlClasses
                        }}
                        value={values.password}
                        onChange={handleChange('password')}
                        inputProps={{
                          startAdornment: (
                            <InputAdornment
                              position="start"
                              className={classes.inputAdornment}
                            >
                              <IconButton
                                aria-label="toggle password visibility"
                                onClick={handleClickShowPassword}
                                onMouseDown={handleMouseDownPassword}
                              >
                                {values.showPassword ? <Visibility /> : <VisibilityOff />}
                              </IconButton>
                          </InputAdornment>
                          ),
                          type: values.showPassword ? "text" : "password",
                          placeholder: "Password..."
                        }}
                      />
                      <FormHelperText error>{errorText.password}</FormHelperText>
                      <div className={classes.center}>
                        <Button color="primary" round onClick={handleLogin}>
                          Log in
                        </Button>
                        <div>
                          <a href="/forgot_password"> Forgot Password?</a>
                        </div>
                        <div>
                          Don&apos;t you have an account? Please
                          <a href="/register"> Join</a>
                        </div>
                      </div>
                    </form>
                  </GridItem>
                </GridContainer>
              </CardBody>
            </Card>
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
