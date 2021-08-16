import React, { useState } from "react";
import { toastr } from "react-redux-toastr";
import { makeStyles } from "@material-ui/core/styles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";
import Face from "@material-ui/icons/Face";
import Email from "@material-ui/icons/Email";
import FormHelperText from "@material-ui/core/FormHelperText";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import styles from "assets/jss/material-dashboard-pro-react/views/registerPageStyle";
import ApiHelper from "helpers/apiHelper";
import { validateEmail } from "helpers/commonHelper";
import { validatePassword } from "helpers/commonHelper";

const useStyles = makeStyles(styles);

export default function RegisterPage() {
  const classes = useStyles();
  const [values, setValues] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errorText, setErrorText] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
    if (event.target.value !== '') {
      setErrorText({...errorText, [prop]: ''});
    }
  };

  const handleRegister = e => {
    e.preventDefault();

    if (values.username === '') {
      setErrorText({...errorText, username: 'Username is required'});
      return;
    }

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

    if (values.password !== values.confirmPassword) {
      setErrorText({...errorText, confirmPassword: 'Password does not match'});
      return;
    }

    if (!validatePassword(values.password)) {
      errorText.password = 'Password should be 6-20 characters, which contain at least one numeric digit, ' +
          'one uppercase and one lowercase letter'
      setErrorText({...errorText, password: errorText.password});
      return;
    }

    ApiHelper.post('/api/auth/register/', {
      username: values.username,
      email: values.email,
      password: values.password,
    }, {}, false).then(() => {
      toastr.success('Success!', 'User was successfully registered.');
      history.push('/login/email_verification');
    }).catch(() => {
      toastr.error('Fail!', 'Please use another email address to register.');
    });
  }


  return (
    <div className={classes.container}>
      <GridContainer justify="center">
        <GridItem xs={12} sm={12} md={6}>
          <Card className={classes.cardSignup}>
            <h2 className={classes.cardTitle}>Register</h2>
            <CardBody>
              <GridContainer justify="center">
                <GridItem xs={12} sm={8} md={8}>
                  <form className={classes.form}>
                    <CustomInput
                      formControlProps={{
                        fullWidth: true,
                        className: classes.customFormControlClasses
                      }}
                      value={values.username}
                      onChange={handleChange('username')}
                      inputProps={{
                        startAdornment: (
                          <InputAdornment
                            position="start"
                            className={classes.inputAdornment}
                          >
                            <Face className={classes.inputAdornmentIcon} />
                          </InputAdornment>
                        ),
                        placeholder: "Username..."
                      }}
                    />
                    <FormHelperText error>{errorText.username}</FormHelperText>
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
                            <Email className={classes.inputAdornmentIcon} />
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
                            <Icon className={classes.inputAdornmentIcon}>
                              lock_outline
                            </Icon>
                          </InputAdornment>
                        ),
                        type: "password",
                        placeholder: "Password..."
                      }}
                    />
                    <FormHelperText error>{errorText.password}</FormHelperText>
                    <CustomInput
                      formControlProps={{
                        fullWidth: true,
                        className: classes.customFormControlClasses
                      }}
                      value={values.confirmPassword}
                      onChange={handleChange('confirmPassword')}
                      inputProps={{
                        startAdornment: (
                          <InputAdornment
                            position="start"
                            className={classes.inputAdornment}
                          >
                            <Icon className={classes.inputAdornmentIcon}>
                              lock_outline
                            </Icon>
                          </InputAdornment>
                        ),
                        type: "password",
                        placeholder: "Confirm Password..."
                      }}
                    />
                    <FormHelperText error>{errorText.confirmPassword}</FormHelperText>
                    <div className={classes.center}>
                      <Button round color="primary" onClick={handleRegister}>
                        Register
                      </Button>
                      <div>You have already account? Please <a href="/login">Login</a></div>
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
