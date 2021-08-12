import LoginPage from "containers/Auth/LoginPage.js";
import RegisterPage from "containers/Auth/RegisterPage.js";

// // @material-ui/icons
// import Apps from "@material-ui/icons/Apps";
// import DashboardIcon from "@material-ui/icons/Dashboard";
// import DateRange from "@material-ui/icons/DateRange";
// import GridOn from "@material-ui/icons/GridOn";
// import Image from "@material-ui/icons/Image";
// import Place from "@material-ui/icons/Place";
// import Timeline from "@material-ui/icons/Timeline";
// import WidgetsIcon from "@material-ui/icons/Widgets";

const dashRoutes = [
  // {
  //   path: "/dashboard",
  //   name: "Dashboard",
  //   rtlName: "لوحة القيادة",
  //   icon: DashboardIcon,
  //   component: Dashboard,
  //   layout: "/admin"
  // },
  {
    path: "/login",
    name: "Login Page",
    rtlName: "هعذاتسجيل الدخول",
    mini: "L",
    rtlMini: "هعذا",
    component: LoginPage,
    layout: "/auth"
  },
  {
    path: "/register",
    name: "Register Page",
    rtlName: "تسجيل",
    mini: "R",
    rtlMini: "صع",
    component: RegisterPage,
    layout: "/auth"
  },
];
export default dashRoutes;
