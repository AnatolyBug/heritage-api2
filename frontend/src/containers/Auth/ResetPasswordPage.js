import React, { useState } from "react";
import { toastr } from "react-redux-toastr";
import { useHistory, useLocation } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";
import FormHelperText from "@material-ui/core/FormHelperText";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import styles from "assets/jss/material-dashboard-pro-react/views/registerPageStyle";
import ApiHelper from "helpers/apiHelper";
import { validatePassword } from "helpers/commonHelper";

const useStyles = makeStyles(styles);

export default function ResetPasswordPage() {
  const classes = useStyles();
  const history = useHistory();
  const [values, setValues] = useState({
    password: '',
    confirmPassword: '',
  });
  const [errorText, setErrorText] = useState({
    password: '',
    confirmPassword: ''
  })

  const useQuery = () => {
    return new URLSearchParams(useLocation().search);
  }

  let query = useQuery();
  const uid = query.get('uid');
  const token = query.get('token');

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
    if (event.target.value !== '') {
      setErrorText({...errorText, [prop]: ''});
    }
  };

  const handleSend = e => {
    e.preventDefault();

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

    ApiHelper.post('/api/auth/reset_password/', {
      uid: uid,
      token: token,
      password: values.password,
    }, {}, false).then(() => {
      toastr.success('Success!', 'Password was successfully reset.');
      history.push('/login');
    }).catch(() => {
      toastr.error('Fail!', 'Failed to reset the password, please try again.');
    });
  }

  return (
    <div className={classes.container}>
      <GridContainer justify="center">
        <GridItem xs={12} sm={12} md={6}>
          <Card className={classes.cardSignup}>
            <h2 className={classes.cardTitle}>Reset Password</h2>
            <CardBody>
              <GridContainer justify="center">
                <GridItem xs={12} sm={8} md={8}>
                  <form className={classes.form}>
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
                      <Button round color="primary" onClick={handleSend}>
                        Send
                      </Button>
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
