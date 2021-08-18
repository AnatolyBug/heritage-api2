import React from "react";
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

const useStyles = makeStyles(styles);

export default function EmailVerificationPage() {
  const classes = useStyles();
  const history = useHistory();

  const handleResend = () => {
    let email = localStorage.getItem('email');
    ApiHelper.post('/api/auth/resend_email/', {
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
            <h2 className={classes.cardTitle}>Verify your email address</h2>
            <CardBody>
              <GridContainer justify="center">
                <GridItem xs={12} sm={8} md={8}>
                  <form className={classes.form}>
                    <FormHelperText>
                      Email has been sent to you, please follow the link in the email to verify your email.
                    </FormHelperText>
                    <div className={classes.center}>
                      <span>You didn&apos;t receive an email? </span>
                      <a onClick={handleResend}>Resend email</a>
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
