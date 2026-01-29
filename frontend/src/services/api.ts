import axios, { type AxiosInstance } from 'axios';
import type {
  Token,
  User,
  Project,
  ProjectCreate,
  Experiment,
  ExperimentCreate,
  Plate,
  PlateCreate,
  Well,
  WellGridItem,
  PaginatedResponse,
} from '../types';

const API_BASE_URL = '/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle 401 errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  async login(email: string, password: string): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await this.client.post<Token>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  }

  async register(email: string, password: string, fullName: string): Promise<User> {
    const response = await this.client.post<User>('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/auth/me');
    return response.data;
  }

  // Projects
  async getProjects(skip = 0, limit = 100): Promise<PaginatedResponse<Project>> {
    const response = await this.client.get<PaginatedResponse<Project>>('/projects', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getProject(id: string): Promise<Project> {
    const response = await this.client.get<Project>(`/projects/${id}`);
    return response.data;
  }

  async createProject(data: ProjectCreate): Promise<Project> {
    const response = await this.client.post<Project>('/projects', data);
    return response.data;
  }

  async updateProject(id: string, data: Partial<ProjectCreate>): Promise<Project> {
    const response = await this.client.patch<Project>(`/projects/${id}`, data);
    return response.data;
  }

  async deleteProject(id: string): Promise<void> {
    await this.client.delete(`/projects/${id}`);
  }

  // Experiments
  async getExperiments(
    projectId: string,
    skip = 0,
    limit = 100
  ): Promise<PaginatedResponse<Experiment>> {
    const response = await this.client.get<PaginatedResponse<Experiment>>(
      `/projects/${projectId}/experiments`,
      { params: { skip, limit } }
    );
    return response.data;
  }

  async getExperiment(projectId: string, id: string): Promise<Experiment> {
    const response = await this.client.get<Experiment>(
      `/projects/${projectId}/experiments/${id}`
    );
    return response.data;
  }

  async createExperiment(projectId: string, data: ExperimentCreate): Promise<Experiment> {
    const response = await this.client.post<Experiment>(
      `/projects/${projectId}/experiments`,
      data
    );
    return response.data;
  }

  async deleteExperiment(projectId: string, id: string): Promise<void> {
    await this.client.delete(`/projects/${projectId}/experiments/${id}`);
  }

  // Plates
  async getPlates(
    experimentId: string,
    skip = 0,
    limit = 100
  ): Promise<PaginatedResponse<Plate>> {
    const response = await this.client.get<PaginatedResponse<Plate>>(
      `/experiments/${experimentId}/plates`,
      { params: { skip, limit } }
    );
    return response.data;
  }

  async getPlate(experimentId: string, id: string): Promise<Plate> {
    const response = await this.client.get<Plate>(
      `/experiments/${experimentId}/plates/${id}`
    );
    return response.data;
  }

  async getPlateGrid(experimentId: string, plateId: string): Promise<WellGridItem[]> {
    const response = await this.client.get<WellGridItem[]>(
      `/experiments/${experimentId}/plates/${plateId}/grid`
    );
    return response.data;
  }

  async createPlate(experimentId: string, data: PlateCreate): Promise<Plate> {
    const response = await this.client.post<Plate>(
      `/experiments/${experimentId}/plates`,
      data
    );
    return response.data;
  }

  async deletePlate(experimentId: string, id: string): Promise<void> {
    await this.client.delete(`/experiments/${experimentId}/plates/${id}`);
  }

  // Wells
  async getWells(plateId: string, skip = 0, limit = 500): Promise<PaginatedResponse<Well>> {
    const response = await this.client.get<PaginatedResponse<Well>>(
      `/plates/${plateId}/wells`,
      { params: { skip, limit } }
    );
    return response.data;
  }

  async getWell(plateId: string, wellId: string): Promise<Well> {
    const response = await this.client.get<Well>(`/plates/${plateId}/wells/${wellId}`);
    return response.data;
  }
}

export const api = new ApiClient();
