import { MainLayout } from './layouts/MainLayout';
import { DashboardPage } from './pages/DashboardPage';

export function App() {
  return (
    <MainLayout>
      {({ selectedLocation, onHealthStatusUpdate }) => (
        <DashboardPage
          selectedLocation={selectedLocation}
          onHealthStatusUpdate={onHealthStatusUpdate}
        />
      )}
    </MainLayout>
  );
}

export default App;
