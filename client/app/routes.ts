import { type RouteConfig, index, route } from "@react-router/dev/routes"

export default [
    route("/", "./components/starting-page/connections-page.tsx"),

    route("/connection/:connectionId/dashboard", "./components/connection/connection-dashboard.tsx")

] satisfies RouteConfig
