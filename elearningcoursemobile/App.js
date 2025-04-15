import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import Home from "./components/Home/Home";
import Login from "./components/User/Login";
import { createStackNavigator } from "@react-navigation/stack";
import Lesson from "./components/Home/Lesson";

const Tab = createBottomTabNavigator();

const Stack = createStackNavigator();
const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="home" component={Home} />
      <Tab.Screen name="lesson" component={Lesson} />
    </Stack.Navigator>
  );
}

const TabNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="index" component={StackNavigator} options={{ tabBarIcon: () => <Icon source="home" size={20} /> }} />
      <Tab.Screen name="login" component={Login} options={{ tabBarIcon: () => <Icon source="account" size={20} /> }} />
    </Tab.Navigator>
  );
}

const App = () => {
  return (
    <NavigationContainer>
      <TabNavigator />
    </NavigationContainer>
  );
}

export default App;