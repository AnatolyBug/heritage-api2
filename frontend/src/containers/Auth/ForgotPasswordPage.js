import React, { useState } from "react";
import { toastr } from "react-redux-toastr";
import { useHistory } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import FormHelperText from "@material-ui/core/FormHelperText";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import styles from "assets/jss/material-dashboard-pro-react/views/registerPageStyle";
import ApiHelper from "helpers/apiHelper";
import CustomInput from "../../components/CustomInput/CustomInput";
import { validateEmail } from "../../helpers/commonHelper";
import Button from "components/CustomButtons/Button";

const useStyles = makeStyles(styles);

export default function ForgotPasswordPage() {
  const classes = useStyles();
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setEmail(event.target.value );
    if (event.target.value !== '') {
      setError('');
    }
  };

  const handleSend = e => {
    e.preventDefault();

    if (email === '') {
      setError('Email is required');
      return;
    }

    if (!validateEmail(email)) {
      setError('Email is invalid');
      return;
    }

    ApiHelper.post('/api/auth/forgot_password/', {
      email: email
    }, {}, false).then(() => {
      toastr.success('Success!', 'Please check your email');
    }).catch(err => {
      if (err.response.data === 'unverified') {
        toastr.error('Fail!', "You haven't verified your email address yet.");
        history.push('/login/email_verification');
      } else {
        toastr.warning('Warning!', 'It is not a verified email.');
      }
    });
  };

  const handleResend = () => {
    let email = localStorage.getItem('email');
    ApiHelper.post('/api/auth/reset_password/', {
      email: email
    }, {}, false).then(res => {
      if (res.data.Status) {
        toastr.success('Success!', 'Please check your email');
      } else {
        toastr.warning('Warning!', 'Your email has been already verified.');
        history.push('/login');
      }
    }).catch(() => {
      toastr.error('Fail!', 'Failed to resend email');
    });
  }

  return (
    <div className={classes.container}>
      <GridContainer justify="center">
        <GridItem xs={12} sm={12} md={6}>
          <Card className={classes.cardSignup}>
            <h2 className={classes.cardTitle}>Forgot Password</h2>
            <CardBody>
              <GridContainer justify="center">
                <GridItem xs={12} sm={8} md={8}>
                  <form className={classes.form}>
                    <p className={classes.center}>Enter verified email address of your account.</p>
                    <CustomInput
                      formControlProps={{
                        fullWidth: true,
                        className: classes.customFormControlClasses
                      }}
                      value={email}
                      onChange={handleChange}
                      inputProps={{
                        placeholder: "Enter your email..."
                      }}
                    />
                    <FormHelperText error>{error}</FormHelperText>
                    <div className={classes.center}>
                      <Button color="primary" round onClick={handleSend}>
                        Send
                      </Button>
                      <div>
                        <span>You didn&apos;t receive an email? </span>
                        <a style={{'cursor': 'pointer'}} onClick={handleResend}>Resend email</a>
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
